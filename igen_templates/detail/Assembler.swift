import UIKit

protocol {{ name }}Assembler {
    {% if use_window %}
    func resolve(window: UIWindow, {{ model_variable }}: {{ model_name }}) -> {{ name }}ViewController
    func resolve(window: UIWindow, {{ model_variable }}: {{ model_name }}) -> {{ name }}ViewModel
    func resolve(window: UIWindow, {{ model_variable }}: {{ model_name }}) -> {{ name }}NavigatorType
    {% else %}
    func resolve(navigationController: UINavigationController, {{ model_variable }}: {{ model_name }}) -> {{ name }}ViewController
    func resolve(navigationController: UINavigationController, {{ model_variable }}: {{ model_name }}) -> {{ name }}ViewModel
    func resolve(navigationController: UINavigationController) -> {{ name }}NavigatorType
    {% endif %}
    func resolve() -> {{ name }}UseCaseType
}

extension {{ name }}Assembler {
    {% if use_window %}
    func resolve(window: UIWindow, {{ model_variable }}: {{ model_name }}) -> {{ name }}ViewController {
        let vc = {{ name }}ViewController.instantiate()
        let vm: {{ name }}ViewModel = resolve(window: window, {{ model_variable }}: {{ model_variable }})
        vc.bindViewModel(to: vm)
        return vc
    }

    func resolve(window: UIWindow, {{ model_variable }}: {{ model_name }}) -> {{ name }}ViewModel {
        return {{ name }}ViewModel(
            navigator: resolve(window: window, {{ model_variable }}: {{ model_variable }}),
            useCase: resolve(),
            {{ model_variable }}: {{ model_variable }}
        )
    }
    {% else %}
    func resolve(navigationController: UINavigationController, {{ model_variable }}: {{ model_name }}) -> {{ name }}ViewController {
        let vc = {{ name }}ViewController.instantiate()
        let vm: {{ name }}ViewModel = resolve(navigationController: navigationController, {{ model_variable }}: {{ model_variable }})
        vc.bindViewModel(to: vm)
        return vc
    }

    func resolve(navigationController: UINavigationController, {{ model_variable }}: {{ model_name }}) -> {{ name }}ViewModel {
        return {{ name }}ViewModel(
            navigator: resolve(navigationController: navigationController),
            useCase: resolve(),
            {{ model_variable }}: {{ model_variable }}
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
