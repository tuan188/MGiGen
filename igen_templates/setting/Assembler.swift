import UIKit

protocol {{ name }}Assembler {
    {% if use_window %}
    func resolve(window: UIWindow) -> {{ name }}ViewController
    func resolve(window: UIWindow) -> {{ name }}ViewModel
    func resolve(window: UIWindow) -> {{ name }}NavigatorType
    {% else %}
    func resolve(navigationController: UINavigationController) -> {{ name }}ViewController
    func resolve(navigationController: UINavigationController) -> {{ name }}ViewModel
    func resolve(navigationController: UINavigationController) -> {{ name }}NavigatorType
    {% endif %}
    func resolve() -> {{ name }}UseCaseType
}

extension {{ name }}Assembler {
    {% if use_window %}
    func resolve(window: UIWindow) -> {{ name }}ViewController {
        let vc = {{ name }}ViewController.instantiate()
        let vm: {{ name }}ViewModel = resolve(window: window)
        vc.bindViewModel(to: vm)
        return vc
    }

    func resolve(window: UIWindow) -> {{ name }}ViewModel {
        return {{ name }}ViewModel(
            navigator: resolve(window: window),
            useCase: resolve()
        )
    }
    {% else %}
    func resolve(navigationController: UINavigationController) -> {{ name }}ViewController {
        let vc = {{ name }}ViewController.instantiate()
        let vm: {{ name }}ViewModel = resolve(navigationController: navigationController)
        vc.bindViewModel(to: vm)
        return vc
    }

    func resolve(navigationController: UINavigationController) -> {{ name }}ViewModel {
        return {{ name }}ViewModel(
            navigator: resolve(navigationController: navigationController),
            useCase: resolve()
        )
    }
    {% endif %}
}

extension {{ name }}Assembler where Self: DefaultAssembler {
    {% if use_window %}
    func resolve(window: UIWindow) -> {{ name }}NavigatorType {
        return {{ name }}Navigator(assembler: self, window: window)
    }
    {% else %}
    func resolve(navigationController: UINavigationController) -> {{ name }}NavigatorType {
        return {{ name }}Navigator(assembler: self, navigationController: navigationController)
    }
    {% endif %}

    func resolve() -> {{ name }}UseCaseType {
        return {{ name }}UseCase()
    }
}
