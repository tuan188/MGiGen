import Dto
import MGArchitecture
import RxCocoa
import RxSwift

struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
    let {{ model_variable }}: {{ model_name }}
}

// MARK: - ViewModelType
extension {{ name }}ViewModel: ViewModel {
    struct Input {
        let loadTrigger: Driver<TriggerType>
        let {{ submit }}Trigger: Driver<Void>
        let cancelTrigger: Driver<Void>
        let dataTrigger: Driver<DataType>
    }

    struct Output {
        {% for p in properties %}
        @Property var {{ p.name }}Validation = ValidationResult.success(())
        {% endfor %}
        @Property var is{{ submit_title }}Enabled = true
        @Property var error: Error?
        @Property var isLoading = false
        @Property var cells: ([CellType], needReload: Bool) = ([], true)
    }

    enum DataType {
        {% for p in properties %}
        case {{ p.name }}({{ p.type.name }})
        {% endfor %}
    }

    struct CellType {
        let dataType: DataType
        let validationResult: ValidationResult
    }

    enum TriggerType {
        case load
        case endEditing
    }

    func transform(_ input: Input, disposeBag: DisposeBag) -> Output {
        let output = Output()

        // Error
        
        let errorTracker = ErrorTracker()
        
        errorTracker
            .asDriver()
            .drive(output.$error)
            .disposed(by: disposeBag)

        // Loading

        let activityIndicator = ActivityIndicator()
        
        activityIndicator
            .asDriver()
            .drive(output.$isLoading)
            .disposed(by: disposeBag)

        // {{ model_name }}

        {% for p in properties %}
        let {{ p.name }} = input.dataTrigger
            .map { data -> {{ p.type.name }}? in
                if case let DataType.{{ p.name }}({{ p.name }}) = data {
                    return {{ p.name }}
                }
                return nil
            }
            .unwrap()
            .startWith(self.{{ model_variable }}.{{ p.name }}){{ '\n' if not loop.last }}
        {% endfor %}

        // Validations

        {% for p in properties %}
        let {{ p.name }}Validation = Driver.combineLatest(
                {{ p.name }},
                input.{{ submit }}Trigger
            )
            .map { $0.0 }
            .map { {{ p.name }} -> ValidationResult in
                self.useCase.validate({{ p.name }}: {{ p.name }})
            }
            .startWith(.success(()))

        {{ p.name }}Validation
            .drive(output.${{ p.name }}Validation)
            .disposed(by: disposeBag){{ '\n' if not loop.last }}
        {% endfor %}

        let is{{ submit_title }}Enabled = Driver.and(
            {% for p in properties %}
            {{ p.name }}Validation.map { $0.isValid }{{ ',' if not loop.last }}
            {% endfor %}
        )
        .startWith(true)

        is{{ submit_title }}Enabled
            .drive(output.$is{{ submit_title }}Enabled)
            .disposed(by: disposeBag)

        // Cells

        let {{ model_variable }} = Driver.combineLatest({% for p in properties %}{{ p.name }}{{ ', ' if not loop.last }}{% endfor %})
            .map { {% for p in properties %}{{ p.name }}{{ ', ' if not loop.last }}{% endfor %} in
                {{ model_name }}(
                    {% for p in properties %}
                    {{ p.name }}: {{ p.name }}{{ ',' if not loop.last }}
                    {% endfor %}
                )
            }

        input.loadTrigger
            .withLatestFrom(Driver.combineLatest({{ model_variable }}, {% for p in properties %}{{ p.name }}Validation{{ ', ' if not loop.last }}{% endfor %}))
            .map { {{ model_variable }}, {% for p in properties %}{{ p.name }}Validation{{ ', ' if not loop.last }}{% endfor %} -> [CellType] in
                return [
                    {% for p in properties %}
                    CellType(dataType: .{{ p.name }}({{ model_variable }}.{{ p.name }}), validationResult: {{ p.name }}Validation){{ ',' if not loop.last }}
                    {% endfor %}
                ]
            }
            .withLatestFrom(input.loadTrigger) {
                ($0, $1 == .load)
            }
            .drive(output.$cells)
            .disposed(by: disposeBag)

        // Actions

        input.cancelTrigger
            .drive(onNext: navigator.dismiss)
            .disposed(by: disposeBag)

        input.{{ submit }}Trigger
            .withLatestFrom(is{{ submit_title }}Enabled)
            .filter { $0 }
            .withLatestFrom({{ model_variable }})
            .flatMapLatest { {{ model_variable }} in
                self.useCase.{{ submit }}({{ model_variable }})
                    .trackError(errorTracker)
                    .trackActivity(activityIndicator)
                    .asDriverOnErrorJustComplete()
                    .map { _ in {{ model_variable }} }
            }
            .drive(onNext: { {{ model_variable }} in
                self.navigator.dismiss()
            })
            .disposed(by: disposeBag)

        return output
    }
}