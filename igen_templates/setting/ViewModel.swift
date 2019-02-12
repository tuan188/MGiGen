struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
}

// MARK: - ViewModelType
extension {{ name }}ViewModel: ViewModelType {
    struct Input {
        let loadTrigger: Driver<Void>
        let select{{ enum.name }}Trigger: Driver<IndexPath>
    }
    
    struct Output {
        let {{ enum.name_variable }}Sections: Driver<[{{ enum.name }}Section]>
        let selected{{ enum.name }}: Driver<Void>
    }

    func transform(_ input: Input) -> Output {
        let {{ enum.name_variable }}Sections = input.loadTrigger
            .map {
                self.{{ enum.name_variable }}Sections()
            }
        
        let selected{{ enum.name }} = input.select{{ enum.name }}Trigger
            .withLatestFrom({{ enum.name_variable }}Sections) { indexPath, {{ enum.name_variable }}Sections in
                {{ enum.name_variable }}Sections[indexPath.section].{{ enum.name_variable }}List[indexPath.row]
            }
            .do(onNext: { {{ enum.name_variable }} in
                switch {{ enum.name_variable }} {
            {% for enum_case in enum.cases %}
                case .{{ enum_case }}:
                    self.navigator.to{{ enum.cases_title[loop.index0] }}()
            {% endfor %}
                }
            })
            .mapToVoid()
        
        return Output(
            {{ enum.name_variable }}Sections: {{ enum.name_variable }}Sections,
            selected{{ enum.name }}: selected{{ enum.name }}
        )
    }
    
    func {{ enum.name_variable }}Sections() -> [{{ enum.name }}Section] {
        return [
            {{ enum.name }}Section(
                title: "Section title", 
                {{ enum.name_variable }}List: [
                {% for enum_case in enum.cases %}
                    .{{ enum_case }}{{ ',' if not loop.last }}
                {% endfor %}
                ]
            )
        ]
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
    
    struct {{ enum.name }}Section {
        let title: String
        let {{ enum.name_variable }}List: [{{ enum.name }}]
    }
}