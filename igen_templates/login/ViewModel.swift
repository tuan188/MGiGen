import MGArchitecture
import RxCocoa
import RxSwift
import ValidatedPropertyKit

struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
}

// MARK: - ViewModel
extension {{ name }}ViewModel: ViewModel {
    struct Input {
        let usernameTrigger: Driver<String>
        let passwordTrigger: Driver<String>
        let loginTrigger: Driver<Void>
    }

    struct Output {
        @Property var usernameValidationMessage = ""
        @Property var passwordValidationMessage = ""
        @Property var isLoginEnabled = true
        @Property var isLoading = false
        @Property var error: Error?
    }

    func transform(_ input: Input, disposeBag: DisposeBag) -> Output {
        let output = Output()
        
        // Error

        let errorTracker = ErrorTracker()

        errorTracker
            .drive(output.$error)
            .disposed(by: disposeBag)

        // Loading
        
        let activityIndicator = ActivityIndicator()
        let isLoading = activityIndicator.asDriver()
        
        isLoading
            .drive(output.$isLoading)
            .disposed(by: disposeBag)

        // Validations
        
        let usernameValidation = Driver.combineLatest(input.usernameTrigger, input.loginTrigger)
            .map { $0.0 }
            .map(useCase.validateUserName(_:))
        
        usernameValidation
            .map { $0.message }
            .drive(output.$usernameValidationMessage)
            .disposed(by: disposeBag)
  
        let passwordValidation = Driver.combineLatest(input.passwordTrigger, input.loginTrigger)
            .map { $0.0 }
            .map(useCase.validatePassword(_:))
        
        passwordValidation
            .map { $0.message }
            .drive(output.$passwordValidationMessage)
            .disposed(by: disposeBag)
        
        let validation = Driver.and(
            usernameValidation.map { $0.isValid },
            passwordValidation.map { $0.isValid }
        )
        .startWith(true)
        
        let isLoginEnabled = Driver.merge(validation, isLoading.not())
        
        isLoginEnabled
            .drive(output.$isLoginEnabled)
            .disposed(by: disposeBag)

        // Login
        
        input.loginTrigger
            .withLatestFrom(isLoginEnabled)
            .filter { $0 }
            .withLatestFrom(Driver.combineLatest(input.usernameTrigger, input.passwordTrigger))
            .flatMapLatest { username, password -> Driver<Void> in
                self.useCase.login(dto: LoginDto(username: username, password: password))
                    .trackError(errorTracker)
                    .trackActivity(activityIndicator)
                    .asDriverOnErrorJustComplete()
            }
            .do(onNext: navigator.toMain)
            .drive()
            .disposed(by: disposeBag)
        
        return output
    }
}
