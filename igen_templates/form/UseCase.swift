protocol {{ name }}UseCaseType {
    {% for p in properties %}
    func validate({{ p.name }}: {{ p.type.name }}) -> ValidationResult
    {% endfor %}
    func {{ submit }}(_ {{ model_variable }}: {{ model_name }}) -> Observable<Void>
}

struct {{ name }}UseCase: {{ name }}UseCaseType {
    {% for p in properties %}
    func validate({{ p.name }}: {{ p.type.name }}) -> ValidationResult {
        return ValidationResult.valid
    }
    
    {% endfor %}
    func {{ submit }}(_ {{ model_variable }}: {{ model_name }}) -> Observable<Void> {
        return Observable.empty()
    }
}