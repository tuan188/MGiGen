struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
}

// MARK: - ViewModelType
extension {{ name }}ViewModel: ViewModelType {
    struct Input {
        let loadTrigger: Driver<Void>
        let reloadTrigger: Driver<Void>
        {% if paging %}
        let loadMoreTrigger: Driver<Void>
        {% endif %}
        let select{{ model_name }}Trigger: Driver<IndexPath>
    }

    struct Output {
        let error: Driver<Error>
        let isLoading: Driver<Bool>
        let isReloading: Driver<Bool>
        {% if paging %}
        let isLoadingMore: Driver<Bool>
        {% endif %}
        let {{ model_variable }}List: Driver<[{{ model_name }}]>
        let selected{{ model_name }}: Driver<Void>
        let isEmpty: Driver<Bool>
    }

    func transform(_ input: Input) -> Output {
        {% if paging %}
        let getPageResult = getPage(
            loadTrigger: input.loadTrigger,
            reloadTrigger: input.reloadTrigger,
            loadMoreTrigger: input.loadMoreTrigger,
            getItems: useCase.get{{ model_name }}List)

        let (page, error, isLoading, isReloading, isLoadingMore) = getPageResult.destructured

        let {{ model_variable }}List = page
            .map { $0.items }
        {% else %}
        let getListResult = getList(
            loadTrigger: input.loadTrigger,
            reloadTrigger: input.reloadTrigger,
            getItems: useCase.get{{ model_name }}List)
        
        let ({{ model_variable }}List, error, isLoading, isReloading) = getListResult.destructured
        {% endif %}

        let selected{{ model_name }} = select(trigger: input.select{{ model_name }}Trigger, items: {{ model_variable }}List)
            .do(onNext: navigator.to{{ model_name }}Detail)
            .mapToVoid()

        let isEmpty = checkIfDataIsEmpty(trigger: Driver.merge(isLoading, isReloading),
                                         items: {{ model_variable }}List)

        return Output(
            error: error,
            isLoading: isLoading,
            isReloading: isReloading,
            {% if paging %}
            isLoadingMore: isLoadingMore,
            {% endif %}
            {{ model_variable }}List: {{ model_variable }}List,
            selected{{ model_name }}: selected{{ model_name }},
            isEmpty: isEmpty
        )
    }
}
