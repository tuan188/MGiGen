struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
}

// MARK: - ViewModelType
extension {{ name }}ViewModel: ViewModelType {
    struct Input {
        let loadTrigger: Driver<Void>
        let reloadTrigger: Driver<Void>
        let loadMoreTrigger: Driver<Void>
        let select{{ model_name }}Trigger: Driver<IndexPath>
    }

    struct Output {
        let error: Driver<Error>
        let isLoading: Driver<Bool>
        let isReloading: Driver<Bool>
        let isLoadingMore: Driver<Bool>
        let {{ model_variable }}List: Driver<[{{ model_name }}]>
        let selected{{ model_name }}: Driver<Void>
        let isEmpty: Driver<Bool>
    }

    func transform(_ input: Input) -> Output {
        let paginationResult = configPagination(
            loadTrigger: input.loadTrigger,
            reloadTrigger: input.reloadTrigger,
            loadMoreTrigger: input.loadMoreTrigger,
            getItems: useCase.get{{ model_name }}List)

        let (page, error, isLoading, isReloading, isLoadingMore) = paginationResult.destructured

        let {{ model_variable }}List = page
            .map { $0.items }

        let selected{{ model_name }} = select(trigger: input.select{{ model_name }}Trigger, items: {{ model_variable }}List)
            .do(onNext: navigator.to{{ model_name }}Detail)
            .mapToVoid()

        let isEmpty = checkIfDataIsEmpty(trigger: Driver.merge(isLoading, isReloading),
                                         items: {{ model_variable }}List)

        return Output(
            error: error,
            isLoading: isLoading,
            isReloading: isReloading,
            isLoadingMore: isLoadingMore,
            {{ model_variable }}List: {{ model_variable }}List,
            selected{{ model_name }}: selected{{ model_name }},
            isEmpty: isEmpty
        )
    }
}
