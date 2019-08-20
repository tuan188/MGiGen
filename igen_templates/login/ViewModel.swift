struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
}

// MARK: - ViewModelType
extension {{ name }}ViewModel: ViewModelType {
    struct Input {
        let usernameTrigger: Driver<String>
        let passwordTrigger: Driver<String>
        let loginTrigger: Driver<Void>
    }

    struct Output {
        let usernameValidation: Driver<ValidationResult>
        let passwordValidation: Driver<ValidationResult>
        let login: Driver<Void>
        let isLoginEnabled: Driver<Bool>
        let isLoading: Driver<Bool>
        let error: Driver<Error>
    }

    func transform(_ input: Input) -> Output {
        let errorTracker = ErrorTracker()
        let activityIndicator = ActivityIndicator()

        let error = errorTracker.asDriver()
        let isLoading = activityIndicator.asDriver()

        let usernameValidation = validate(
            object: input.usernameTrigger,
            trigger: input.loginTrigger,
            validator: useCase.validate(username:)
        )

        let passwordValidation = validate(
            object: input.passwordTrigger,
            trigger: input.loginTrigger,
            validator: useCase.validate(password:)
        )

        let validation = Driver.and(
            usernameValidation.map { $0.isValid },
            passwordValidation.map { $0.isValid }
        )
        .startWith(true)

        let isLoginEnabled = Driver.merge(validation, isLoading.not())

        let login = input.loginTrigger
            .withLatestFrom(isLoginEnabled)
            .filter { $0 }
            .withLatestFrom(Driver.combineLatest(input.usernameTrigger, input.passwordTrigger))
            .flatMapLatest { username, password -> Driver<Void> in
                self.useCase.login(username: username, password: password)
                    .trackError(errorTracker)
                    .trackActivity(activityIndicator)
                    .asDriverOnErrorJustComplete()
            }
            .do(onNext: navigator.toMain)

        return Output(
            usernameValidation: usernameValidation,
            passwordValidation: passwordValidation,
            login: login,
            isLoginEnabled: isLoginEnabled,
            isLoading: isLoading,
            error: error
        )
    }
}

extension ViewModelType {
    func validate<T>(object: Driver<T>,
                     trigger: Driver<Void>,
                     validator: @escaping (T) -> ValidationResult) -> Driver<ValidationResult> {
        return Driver.combineLatest(object, trigger)
            .map { $0.0 }
            .map { validator($0) }
            .startWith(.valid)
    }
}
