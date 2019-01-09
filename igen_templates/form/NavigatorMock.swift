@testable import {{ project }}

final class {{ name }}NavigatorMock: {{ name }}NavigatorType {
    
    // MARK: - dismiss

    var dismissCalled = false

    func dismiss() {
        dismissCalled = true
    }
    
}