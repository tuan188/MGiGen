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
        let cells: Driver<[CellType]>
    }

    enum CellType {
    {% for p in properties %}
        case {{ p.name }}({{ p.type.name }})
    {% endfor %}
    }

    func transform(_ input: Input) -> Output {
        let {{ model_variable }} = input.loadTrigger
            .map { self.{{ model_variable }} }

        let cells = {{ model_variable }}
            .map { {{ model_variable }} -> [CellType] in
                var cells = [CellType]()
            {% for p in properties %}
                cells.append(CellType.{{ p.name }}({{ model_variable }}.{{ p.name }}))
            {% endfor %}
                return cells
            }
            
        return Output(cells: cells)
    }
}
