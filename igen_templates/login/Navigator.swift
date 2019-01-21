protocol {{ name }}NavigatorType {
    func toMain()
}

struct {{ name }}Navigator: {{ name }}NavigatorType {
    unowned let assembler: Assembler
    unowned let navigationController: UINavigationController
    
    func toMain() {
        
    }
}
