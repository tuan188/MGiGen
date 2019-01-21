protocol {{ name }}UseCaseType {
    func validate(username: String) -> ValidationResult
    func validate(password: String) -> ValidationResult
    func login(username: String, password: String) -> Observable<Void>
}

struct {{ name }}UseCase: {{ name }}UseCaseType {
    func validate(username: String) -> ValidationResult {
        return ValidationResult.valid
    }
    
    func validate(password: String) -> ValidationResult {
        return ValidationResult.valid
    }
    
    func login(username: String, password: String) -> Observable<Void> {
        return Observable.just(())
    }
}
