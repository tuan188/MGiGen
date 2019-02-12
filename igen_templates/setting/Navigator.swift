protocol {{ name }}NavigatorType {
{% for enum_case in enum.cases_title %}
    func to{{ enum_case }}()
{% endfor %}
}

struct {{ name }}Navigator: {{ name }}NavigatorType {
    unowned let assembler: Assembler
    {% if use_window %}
    unowned let window: UIWindow
    {% else %}
    unowned let navigationController: UINavigationController
    {% endif %}

{% for enum_case in enum.cases_title %}
    func to{{ enum_case }}() {

    }{{ '\n' if not loop.last }}
{% endfor %}
}
