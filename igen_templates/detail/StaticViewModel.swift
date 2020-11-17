import MGArchitecture
import RxCocoa
import RxSwift

struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
    let {{ model_variable }}: {{ model_name }}
}

// MARK: - ViewModel
extension {{ name }}ViewModel: ViewModel {
    struct Input {
        let loadTrigger: Driver<Void>
    }

    struct Output {
        {% for p in properties %}
        @Property var {{ p.name }} = {{ p.type.default_value }}
        {% endfor %}
    }

    func transform(_ input: Input, disposeBag: DisposeBag) -> Output {
        let output = Output()

        let {{ model_variable }} = input.loadTrigger
            .map { self.{{ model_variable }} }

        {% for p in properties %}
        {{ model_variable }}.map { $0.{{ p.name }} }
            .drive(output.${{ p.name }})
            .disposed(by: disposeBag){{ '\n' if not loop.last }}
        {% endfor %}
    
        return output
    }
}
