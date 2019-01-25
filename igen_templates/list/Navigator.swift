protocol {{ name }}NavigatorType {
    func to{{ model_name }}Detail({{ model_variable }}: {{ model_name }})
}

struct {{ name }}Navigator: {{ name }}NavigatorType {
    unowned let assembler: Assembler
    {% if use_window %}
    unowned let window: UIWindow
    {% else %}
    unowned let navigationController: UINavigationController
    {% endif %}

    func to{{ model_name }}Detail({{ model_variable }}: {{ model_name }}) {

    }
}

