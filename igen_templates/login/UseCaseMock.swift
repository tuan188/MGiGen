@testable import {{ project }}
import RxSwift

final class {{ name }}UseCaseMock: {{ name }}UseCaseType {
    // MARK: - validate username
    
    var validateUsernameCalled = false
    var validateUsernameReturnValue = ValidationResult.valid
    
    func validate(username: String) -> ValidationResult {
        validateUsernameCalled = true
        return validateUsernameReturnValue
    }
    
    // MARK: - validate password
    
    var validatePasswordCalled = false
    var validatePasswordReturnValue = ValidationResult.valid
    
    func validate(password: String) -> ValidationResult {
        validatePasswordCalled = true
        return validatePasswordReturnValue
    }
    
    // MARK: - login
    
    var loginCalled = false
    var loginReturnValue = Observable.just(())
    
    func login(username: String, password: String) -> Observable<Void> {
        loginCalled = true
        return loginReturnValue
    }

}
