struct {{name}}ViewModel: ViewModelType {
    struct Input {
        let loadTrigger: Driver<Void>
    }

    struct Output {
        let cells: Driver<[CellType]>
    }

    enum CellType {
    {% for property in properties %}
        case {{property.name}}({{property.type.name}})
    {% endfor %}
    }

    let navigator: {{name}}NavigatorType
    let useCase: {{name}}UseCaseType
    let {{model_variable}}: {{model_name}}

    func transform(_ input: Input) -> Output {
        let {{model_variable}} = input.loadTrigger
            .map { self.{{model_variable}} }
        let cells = {{model_variable}}
            .map { {{model_variable}} -> [CellType] in
                var cells = [CellType]()
            {% for property in properties %}
                cells.append(CellType.{{property.name}}({{model_variable}}.{{property.name}}))
            {% endfor %}
                return cells
            }
        return Output(cells: cells)
    }
}
