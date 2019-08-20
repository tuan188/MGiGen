struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
    let {{ model_variable }}: {{ model_name }}
}

// MARK: - ViewModelType
extension {{ name }}ViewModel: ViewModelType {
    struct Input {
        let loadTrigger: Driver<Void>
        {% for p in properties %}
        let {{ p.name }}Trigger: Driver<{{ p.type.name }}>
        {% endfor %}
        let {{ submit }}Trigger: Driver<Void>
        let cancelTrigger: Driver<Void>
    }

    struct Output {
        {% for p in properties %}
        let {{ p.name }}: Driver<{{ p.type.name }}>
        {% endfor %}
        {% for p in properties %}
        let {{ p.name }}Validation: Driver<ValidationResult>
        {% endfor %}
        let is{{ submit_title }}Enabled: Driver<Bool>
        let {{ submit }}: Driver<Void>
        let cancel: Driver<Void>
        let error: Driver<Error>
        let isLoading: Driver<Bool>
    }

    func transform(_ input: Input) -> Output {
        let errorTracker = ErrorTracker()
        let error = errorTracker.asDriver()

        let activityIndicator = ActivityIndicator()
        let isLoading = activityIndicator.asDriver()

        // Properties
        {% for p in properties %}
        let {{ p.name }} = input.loadTrigger
            .map { self.{{ model_variable }}.{{ p.name }} }{{ '\n' if not loop.last }}
        {% endfor %}

        // Validations
        {% for p in properties %}
        let {{ p.name }}Validation = Driver.combineLatest(
                input.{{ p.name }}Trigger,
                input.{{ submit }}Trigger
            )
            .map { $0.0 }
            .map { {{ p.name }} -> ValidationResult in
                self.useCase.validate({{ p.name }}: {{ p.name }})
            }{{ '\n' if not loop.last }}
        {% endfor %}

        let is{{ submit_title }}Enabled = Driver.and(
            {% for p in properties %}
            {{ p.name }}Validation.map { $0.isValid }{{ ',' if not loop.last }}
            {% endfor %}
        )
        .startWith(true)

        let {{ submit }} = input.{{ submit }}Trigger
            .withLatestFrom(is{{ submit_title }}Enabled)
            .filter { $0 }
            .withLatestFrom(Driver.combineLatest(
                {% for p in properties %}
                input.{{ p.name }}Trigger{{ ',' if not loop.last }}
                {% endfor %}
            ))
            .flatMapLatest { params -> Driver<{{ model_name }}> in
                let ({% for p in properties %}{{ p.name }}{{ ', ' if not loop.last }}{% endfor %}) = params
                let {{ model_variable }} = self.{{ model_variable }}.with {
                    {% for p in properties %}
                    $0.{{ p.name }} = {{ p.name }}
                    {% endfor %}
                }
                return self.useCase.{{ submit }}({{ model_variable }})
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

        let cancel = input.cancelTrigger
            .do(onNext: navigator.dismiss)

        return Output(
            {% for p in properties %}
            {{ p.name }}: {{ p.name }},
            {% endfor %}
            {% for p in properties %}
            {{ p.name }}Validation: {{ p.name }}Validation,
            {% endfor %}
            is{{ submit_title }}Enabled: is{{ submit_title }}Enabled,
            {{ submit }}: {{ submit }},
            cancel: cancel,
            error: error,
            isLoading: isLoading
        )
    }
}