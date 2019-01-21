@testable import {{ project }}
import XCTest
import RxSwift
import RxBlocking

final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!
    
    private var disposeBag: DisposeBag!
    
    private let usernameTrigger = PublishSubject<String>()
    private let passwordTrigger = PublishSubject<String>()
    private let loginTrigger = PublishSubject<Void>()
    
    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase)
        
        input = {{ name }}ViewModel.Input(
            usernameTrigger: usernameTrigger.asDriverOnErrorJustComplete(),
            passwordTrigger: passwordTrigger.asDriverOnErrorJustComplete(),
            loginTrigger: loginTrigger.asDriverOnErrorJustComplete()
        )
        
        output = viewModel.transform(input)
        
        disposeBag = DisposeBag()
        
        output.usernameValidation.drive().disposed(by: disposeBag)
        output.passwordValidation.drive().disposed(by: disposeBag)
        output.login.drive().disposed(by: disposeBag)
        output.loginEnabled.drive().disposed(by: disposeBag)
        output.loading.drive().disposed(by: disposeBag)
        output.error.drive().disposed(by: disposeBag)
    }
    
    func test_loginTrigger_validateUsername() {
        // act
        usernameTrigger.onNext("")
        loginTrigger.onNext(())
        
        // assert
        XCTAssert(useCase.validateUsernameCalled)
    }
    
    func test_loginTrigger_validatePassword() {
        // act
        passwordTrigger.onNext("")
        loginTrigger.onNext(())
        
        // assert
        XCTAssert(useCase.validatePasswordCalled)
    }
    
    func test_loginTrigger_validateUsernameFailed_disable{{ name }}() {
        // arrange
        useCase.validateUsernameReturnValue = ValidationResult.invalid([TestError()])
        
        // act
        usernameTrigger.onNext("")
        passwordTrigger.onNext("")
        loginTrigger.onNext(())
        
        let loginEnabled = try? output.loginEnabled.toBlocking(timeout: 1).first()
        
        // assert
        XCTAssertEqual(loginEnabled, false)
    }
    
    func test_loginTrigger_validatePasswordFailed_disable{{ name }}() {
        // arrange
        useCase.validatePasswordReturnValue = ValidationResult.invalid([TestError()])
        
        // act
        usernameTrigger.onNext("")
        passwordTrigger.onNext("")
        loginTrigger.onNext(())
        
        let loginEnabled = try? output.loginEnabled.toBlocking(timeout: 1).first()
        
        // assert
        XCTAssertEqual(loginEnabled, false)
    }
    
    func test_loginTrigger_disable{{ name }}_not{{ name }}() {
        // arrange
        useCase.validatePasswordReturnValue = ValidationResult.invalid([TestError()])
        
        // act
        usernameTrigger.onNext("")
        passwordTrigger.onNext("")
        loginTrigger.onNext(())
        
        // assert
        XCTAssertFalse(useCase.loginCalled)
    }
    
    func test_loginTrigger_login() {
        // act
        usernameTrigger.onNext("")
        passwordTrigger.onNext("")
        loginTrigger.onNext(())
        
        // assert
        XCTAssert(useCase.loginCalled)
        XCTAssert(navigator.toMainCalled)
    }
    
    func test_loginTrigger_login_showLoading() {
        // arrange
        let loginReturnValue = Observable<Void>.never()
        useCase.loginReturnValue = loginReturnValue
        
        // act
        usernameTrigger.onNext("")
        passwordTrigger.onNext("")
        loginTrigger.onNext(())
        
        let loading = try? output.loading.toBlocking(timeout: 1).first()
        
        // assert
        XCTAssert(useCase.loginCalled)
        XCTAssertEqual(loading, true)
    }
    
    func test_loginTrigger_loading_disable{{ name }}() {
        // arrange
        let loginReturnValue = Observable<Void>.never()
        useCase.loginReturnValue = loginReturnValue
        
        // act
        usernameTrigger.onNext("")
        passwordTrigger.onNext("")
        loginTrigger.onNext(())
        
        let loading = try? output.loading.toBlocking(timeout: 1).first()
        let loginEnabled = try? output.loginEnabled.toBlocking(timeout: 1).first()
        
        // assert
        XCTAssert(useCase.loginCalled)
        XCTAssertEqual(loading, true)
        XCTAssertEqual(loginEnabled, false)
    }
    
    func test_loginTrigger_login_failedShowError() {
        // arrange
        let loginReturnValue = PublishSubject<Void>()
        useCase.loginReturnValue = loginReturnValue
        
        // act
        usernameTrigger.onNext("")
        passwordTrigger.onNext("")
        loginTrigger.onNext(())
        loginReturnValue.onError(TestError())
        
        let error = try? output.error.toBlocking(timeout: 1).first()
        
        // assert
        XCTAssert(useCase.loginCalled)
        XCTAssert(error is TestError)
        XCTAssertFalse(navigator.toMainCalled)
    }
    
}
