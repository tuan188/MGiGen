protocol {{ name }}NavigatorType {
    func toMain()
}

struct {{ name }}Navigator: {{ name }}NavigatorType {
    unowned let assembler: Assembler
    {% if use_window %}
    unowned let window: UIWindow
    {% else %}
    unowned let navigationController: UINavigationController
    {% endif %}
    
    func toMain() {
        
    }
}
