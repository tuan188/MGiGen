@testable import {{ project }}
import RxSwift

final class {{ name }}UseCaseMock: {{ name }}UseCaseType {
    
    {% for p in properties %}
    // MARK: - validate {{ p.name }}

    var validate{{ p.name_title }}Called = false
    var validate{{ p.name_title }}ReturnValue = ValidationResult.valid
    
    func validate({{ p.name }}: {{ p.type.name }}) -> ValidationResult {
        validate{{ p.name_title }}Called = true
        return validate{{ p.name_title }}ReturnValue
    } {{ '\n' if not loop.last }}
    {% endfor %}
    
    // MARK: - {{ submit }}
    
    var {{ submit }}Called = false

    var {{ submit }}ReturnValue = Observable.just(())
    
    func {{ submit }}(_ {{ model_variable }}: {{ model_name }}) -> Observable<Void> {
        {{ submit }}Called = true
        return {{ submit }}ReturnValue
    }

}