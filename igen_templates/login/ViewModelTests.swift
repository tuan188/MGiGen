@testable import {{ project }}
import RxSwift
import RxTest
import ValidatedPropertyKit
import XCTest

final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!
    private var disposeBag: DisposeBag!
 
    // Triggers
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
        
        disposeBag = DisposeBag()
        output = viewModel.transform(input, disposeBag: disposeBag)
    }
    
    func test_loginTrigger_validateUsername() {
        // act
        usernameTrigger.onNext("foobar")
        loginTrigger.onNext(())
        
        // assert
        XCTAssert(useCase.validateUserNameCalled)
    }
    
    func test_loginTrigger_validatePassword() {
        // act
        passwordTrigger.onNext("foobar")
        loginTrigger.onNext(())
        
        // assert
        XCTAssert(useCase.validatePasswordCalled)
    }
    
    func test_loginTrigger_validateUsernameFailed_disableLogin() {
        // arrange
        useCase.validateUserNameReturnValue = .failure(ValidationError(message: "invalid username"))
        
        // act
        usernameTrigger.onNext("foobar")
        passwordTrigger.onNext("foobar")
        loginTrigger.onNext(())
        
        // assert
        XCTAssertEqual(output.isLoginEnabled, false)
        XCTAssertFalse(useCase.loginCalled)
    }
    
    func test_loginTrigger_validatePasswordFailed_disableLogin() {
        // arrange
        useCase.validatePasswordReturnValue = .failure(ValidationError(message: "invalid password"))
        
        // act
        usernameTrigger.onNext("foobar")
        passwordTrigger.onNext("foobar")
        loginTrigger.onNext(())
        
        // assert
        XCTAssertEqual(output.isLoginEnabled, false)
        XCTAssertFalse(useCase.loginCalled)
    }
    
    func test_loginTrigger_login() {
        // act
        usernameTrigger.onNext("foobar")
        passwordTrigger.onNext("foobar")
        loginTrigger.onNext(())
        
        // assert
        XCTAssert(useCase.loginCalled)
        XCTAssert(navigator.toMainCalled)
    }
    
    func test_loginTrigger_login_showLoading() {
        // arrange
        useCase.loginReturnValue = Observable<Void>.never()
        
        // act
        usernameTrigger.onNext("foobar")
        passwordTrigger.onNext("foobar")
        loginTrigger.onNext(())
        
        // assert
        XCTAssert(useCase.loginCalled)
        XCTAssertEqual(output.isLoading, true)
        XCTAssertEqual(output.isLoginEnabled, false)
    }
    
    func test_loginTrigger_login_failedShowError() {
        // arrange
        useCase.loginReturnValue = Observable.error(TestError())
        
        // act
        usernameTrigger.onNext("foobar")
        passwordTrigger.onNext("foobar")
        loginTrigger.onNext(())
        
        // assert
        XCTAssert(useCase.loginCalled)
        XCTAssert(output.error is TestError)
        XCTAssertFalse(navigator.toMainCalled)
    }
}
