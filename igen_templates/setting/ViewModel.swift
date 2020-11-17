import MGArchitecture
import RxCocoa
import RxSwift

struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
}

// MARK: - ViewModelType
extension {{ name }}ViewModel: ViewModel {
    struct Input {
        let loadTrigger: Driver<Void>
        let select{{ enum.name }}Trigger: Driver<IndexPath>
    }
    
    struct Output {
        @Property var {{ enum.name_variable }}List = [{{ enum.name }}]()
    }

    func transform(_ input: Input, disposeBag: DisposeBag) -> Output {
        let output = Output()

        let {{ enum.name_variable }}List = input.loadTrigger
            .map {
                {{ enum.name }}.allCases
            }

        {{ enum.name_variable }}List
            .drive(output.${{ enum.name_variable }}List)
            .disposed(by: disposeBag)
        
        input.select{{ enum.name }}Trigger
            .withLatestFrom({{ enum.name_variable }}List) { indexPath, {{ enum.name_variable }}List in
                {{ enum.name_variable }}List[indexPath.row]
            }
            .drive(onNext: { {{ enum.name_variable }} in
                switch {{ enum.name_variable }} {
                {% for enum_case in enum.cases %}
                case .{{ enum_case }}:
                    self.navigator.to{{ enum.cases_title[loop.index0] }}()
                {% endfor %}
                }
            })
            .disposed(by: disposeBag)
        
        return output
    }
}

extension {{ name }}ViewModel {
    enum {{ enum.name }}: Int, CustomStringConvertible, CaseIterable {
        {% for enum_case in enum.cases %}
        case {{ enum_case }}
        {% endfor %}
        
        var description: String {
            switch self {
            {% for enum_case in enum.cases %}
            case .{{ enum_case }}:
                return "{{ enum.cases_title[loop.index0] }}"
            {% endfor %}
            }
        }
    }
}