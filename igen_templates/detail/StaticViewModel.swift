struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
    let {{ model_variable }}: {{ model_name }}
}

// MARK: - ViewModelType
extension {{ name }}ViewModel: ViewModelType {
    struct Input {
        let loadTrigger: Driver<Void>
    }

    struct Output {
    {% for p in properties %}
        let {{ p.name }}: Driver<{{ p.type.name }}>
    {% endfor %}
    }

    func transform(_ input: Input) -> Output {
        let {{ model_variable }} = input.loadTrigger
            .map { self.{{ model_variable }} }

    {% for p in properties %}
        let {{ p.name }} = {{ model_variable }}.map { $0.{{ p.name }} }
    {% endfor %}
    
        return Output(
        {% for p in properties %}
            {{ p.name }}: {{ p.name }}{{ "," if not loop.last }}
        {% endfor %}
        )
    }
}
