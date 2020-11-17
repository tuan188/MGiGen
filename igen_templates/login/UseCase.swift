import Dto
import RxSwift
import ValidatedPropertyKit

protocol {{ name }}UseCaseType {
    func validateUserName(_ username: String) -> ValidationResult
    func validatePassword(_ password: String) -> ValidationResult
    func login(dto: LoginDto) -> Observable<Void>
}

struct {{ name }}UseCase: {{ name }}UseCaseType {
    func validateUserName(_ username: String) -> ValidationResult {
        return .success(())
    }
    
    func validatePassword(_ password: String) -> ValidationResult {
        return .success(())
    }
    
    func login(dto: LoginDto) -> Observable<Void> {
        return Observable.empty()
    }
}