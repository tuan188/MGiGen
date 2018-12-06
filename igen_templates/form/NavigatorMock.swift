@testable import {{ project }}

final class {{ name }}NavigatorMock: {{ name }}NavigatorType {
    
    // MARK: - dismiss

    var dismiss_Called = false

    func dismiss() {
        dismiss_Called = true
    }
    
}