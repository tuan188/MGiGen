@testable import {{ project }}

final class {{ name }}NavigatorMock: {{ name }}NavigatorType {
{% for menu_case in enum.cases_title %}
        
    // MARK: - to{{ menu_case }}
    
    var to{{ menu_case }}Called = false
    
    func to{{ menu_case }}() {
        to{{ menu_case }}Called = true
    }
{% endfor %}
}
