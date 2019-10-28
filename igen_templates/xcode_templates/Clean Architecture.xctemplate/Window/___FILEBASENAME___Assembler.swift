//___FILEHEADER___

protocol ___VARIABLE_productName___Assembler {
    func resolve(window: UIWindow) -> ___VARIABLE_productName___ViewController
    func resolve(window: UIWindow) -> ___VARIABLE_productName___ViewModel
    func resolve(window: UIWindow) -> ___VARIABLE_productName___NavigatorType
    func resolve() -> ___VARIABLE_productName___UseCaseType
}

extension ___VARIABLE_productName___Assembler {
    func resolve(window: UIWindow) -> ___VARIABLE_productName___ViewController {
        let vc = ___VARIABLE_productName___ViewController.instantiate()
        let vm: ___VARIABLE_productName___ViewModel = resolve(window: window)
        vc.bindViewModel(to: vm)
        return vc
    }
    
    func resolve(window: UIWindow) -> ___VARIABLE_productName___ViewModel {
        return ___VARIABLE_productName___ViewModel(
            navigator: resolve(window: window),
            useCase: resolve()
        )
    }
}

extension ___VARIABLE_productName___Assembler where Self: DefaultAssembler {
    func resolve(window: UIWindow) -> ___VARIABLE_productName___NavigatorType {
        return ___VARIABLE_productName___Navigator(assembler: self, window: window)
    }
    
    func resolve() -> ___VARIABLE_productName___UseCaseType {
        return ___VARIABLE_productName___UseCase()
    }
}
