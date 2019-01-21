@testable import {{ project }}

final class {{ name }}NavigatorMock: {{ name }}NavigatorType {
    // MARK: - toMain
    
    var toMainCalled = false
    
    func toMain() {
        toMainCalled = true
    }
}