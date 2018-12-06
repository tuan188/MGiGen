protocol {{ name }}NavigatorType {
    func dismiss()
}

struct {{ name }}Navigator: {{ name }}NavigatorType {
    unowned let assembler: Assembler
    unowned let navigationController: UINavigationController

    func dismiss() {
        navigationController.dismiss(animated: true, completion: nil)
    }
}
