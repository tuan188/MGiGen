import Dto
import ValidatedPropertyKit

struct LoginDto: Dto {
    @Validated(.nonEmpty)
    var username: String? = ""  // swiftlint:disable:this let_var_whitespace
    
    @Validated(.nonEmpty)
    var password: String? = ""  // swiftlint:disable:this let_var_whitespace
    
    var validatedProperties: [ValidatedProperty] {
        return [_username, _password]
    }
}

extension LoginDto {
    init(username: String, password: String) {
        self.username = username
        self.password = password
    }
    
    static func validateUserName(_ username: String) -> Result<String, ValidationError> {
        LoginDto()._username.isValid(value: username)
    }
    
    static func validatePassword(_ password: String) -> Result<String, ValidationError> {
        LoginDto()._password.isValid(value: password)
    }
}