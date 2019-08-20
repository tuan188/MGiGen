struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
    let {{ model_variable }}: {{ model_name }}
}

// MARK: - ViewModelType
extension {{ name }}ViewModel: ViewModelType {
    struct Input {
        let loadTrigger: Driver<TriggerType>
        let {{ submit }}Trigger: Driver<Void>
        let cancelTrigger: Driver<Void>
        let dataTrigger: Driver<DataType>
    }

    struct Output {
        {% for p in properties %}
        let {{ p.name }}Validation: Driver<ValidationResult>
        {% endfor %}
        let is{{ submit_title }}Enabled: Driver<Bool>
        let {{ submit }}: Driver<Void>
        let cancel: Driver<Void>
        let error: Driver<Error>
        let isLoading: Driver<Bool>
        let cells: Driver<([CellType], Bool)>
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

    func transform(_ input: Input) -> Output {
        let errorTracker = ErrorTracker()
        let error = errorTracker.asDriver()

        let activityIndicator = ActivityIndicator()
        let isLoading = activityIndicator.asDriver()

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
            .startWith(.valid){{ '\n' if not loop.last }}
        {% endfor %}

        let is{{ submit_title }}Enabled = Driver.and(
            {% for p in properties %}
            {{ p.name }}Validation.map { $0.isValid }{{ ',' if not loop.last }}
            {% endfor %}
        )
        .startWith(true)

        let {{ model_variable }} = Driver.combineLatest({% for p in properties %}{{ p.name }}{{ ', ' if not loop.last }}{% endfor %})
            .map { {% for p in properties %}{{ p.name }}{{ ', ' if not loop.last }}{% endfor %} in
                {{ model_name }}(
                    {% for p in properties %}
                    {{ p.name }}: {{ p.name }}{{ ',' if not loop.last }}
                    {% endfor %}
                )
            }

        let cells = input.loadTrigger
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

        let cancel = input.cancelTrigger
            .do(onNext: navigator.dismiss)

        let {{ submit }} = input.{{ submit }}Trigger
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
            .do(onNext: { {{ model_variable }} in
                // notify then dismiss
                self.navigator.dismiss()
            })
            .mapToVoid()

        return Output(
            {% for p in properties %}
            {{ p.name }}Validation: {{ p.name }}Validation,
            {% endfor %}
            is{{ submit_title }}Enabled: is{{ submit_title }}Enabled,
            {{ submit }}: {{ submit }},
            cancel: cancel,
            error: error,
            isLoading: isLoading,
            cells: cells
        )
    }
}