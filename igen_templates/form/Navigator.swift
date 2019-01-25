protocol {{ name }}NavigatorType {
    func dismiss()
}

struct {{ name }}Navigator: {{ name }}NavigatorType {
    unowned let assembler: Assembler
    {% if use_window %}
    unowned let window: UIWindow
    {% else %}
    unowned let navigationController: UINavigationController
    {% endif %}

    func dismiss() {
        navigationController.dismiss(animated: true, completion: nil)
    }
}
