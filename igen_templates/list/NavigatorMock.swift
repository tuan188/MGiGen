@testable import {{ project }}

final class {{ name }}NavigatorMock: {{ name }}NavigatorType {
    
    // MARK: - to{{ model_name }}Detail

    var to{{ model_name }}DetailCalled = false

    func to{{ model_name }}Detail({{ model_variable }}: {{ model_name }}) {
        to{{ model_name }}DetailCalled = true
    }
}
