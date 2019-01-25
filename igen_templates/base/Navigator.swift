protocol {{ name }}NavigatorType {

}

struct {{ name }}Navigator: {{ name }}NavigatorType {
    unowned let assembler: Assembler
    {% if use_window %}
    unowned let window: UIWindow
    {% else %}
    unowned let navigationController: UINavigationController
    {% endif %}
}
