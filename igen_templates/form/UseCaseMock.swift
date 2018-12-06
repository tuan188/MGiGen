@testable import {{ project }}
import RxSwift

final class {{ name }}UseCaseMock: {{ name }}UseCaseType {
    
{% for p in properties %}
    // MARK: - validate {{ p.name }}

    var validate{{ p.name_title }}_Called = false
    var validate{{ p.name_title }}_ReturnValue: ValidationResult = ValidationResult.valid
    
    func validate({{ p.name }}: {{ p.type.name }}) -> ValidationResult {
        validate{{ p.name_title }}_Called = true
        return validate{{ p.name_title }}_ReturnValue
    } {{ '\n' if not loop.last }}
{% endfor %}
    
    // MARK: - {{ submit }}
    
    var {{ submit }}_Called = false

    var {{ submit }}_ReturnValue: Observable<Void> = Observable.just(())
    
    func {{ submit }}(_ {{ model_variable }}: {{ model_name }}) -> Observable<Void> {
        {{ submit }}_Called = true
        return {{ submit }}_ReturnValue
    }

}