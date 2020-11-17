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
        @Property var cells = [CellType]()
    }

    enum CellType {
        {% for p in properties %}
        case {{ p.name }}({{ p.type.name }})
        {% endfor %}
    }

    func transform(_ input: Input, disposeBag: DisposeBag) -> Output {
        let output = Output()

        input.loadTrigger
            .map { self.{{ model_variable }} }
            .map { {{ model_variable }} -> [CellType] in
                return [
                    {% for p in properties %}
                    CellType.{{ p.name }}({{ model_variable }}.{{ p.name }}){{ ',' if not loop.last }}
                    {% endfor %}
                ]
            }
            .drive(output.$cells)
            .disposed(by: disposeBag)
            
        return output
    }
}
