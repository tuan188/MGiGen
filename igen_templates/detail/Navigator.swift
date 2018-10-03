protocol {{ name }}NavigatorType {

}

struct {{ name }}Navigator: {{ name }}NavigatorType {
    unowned let assembler: Assembler
    unowned let navigationController: UINavigationController
}
