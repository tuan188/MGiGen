protocol {{ name }}NavigatorType {
    func to{{ model_name }}Detail({{ model_variable }}: {{ model_name }})
}

struct {{ name }}Navigator: {{ name }}NavigatorType {
    unowned let assembler: Assembler
    unowned let navigationController: UINavigationController

    func to{{ model_name }}Detail({{ model_variable }}: {{ model_name }}) {

    }
}

