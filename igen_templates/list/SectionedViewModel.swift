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
        let {{ model_variable }}Sections: Driver<[{{ model_name }}Section]>
        let selected{{ model_name }}: Driver<Void>
        let isEmpty: Driver<Bool>
    }

    struct {{ model_name }}Section {
        let header: String
        let {{ model_variable }}List: [{{ model_name }}]
    }

    func transform(_ input: Input) -> Output {
        let paginationResult = configPagination(
            loadTrigger: input.loadTrigger,
            reloadTrigger: input.reloadTrigger,
            loadMoreTrigger: input.loadMoreTrigger,
            getItems: useCase.get{{ model_name }}List)

        let (page, error, isLoading, isReloading, isLoadingMore) = paginationResult.destructured

        let {{ model_variable }}Sections = page
            .map { $0.items }
            .map { [{{ model_name }}Section(header: "Section1", {{ model_variable }}List: $0)] }

        let selected{{ model_name }} = input.select{{ model_name }}Trigger
            .withLatestFrom({{ model_variable }}Sections) {
                return ($0, $1)
            }
            .map { indexPath, {{ model_variable }}Sections -> {{ model_name }} in
                return {{ model_variable }}Sections[indexPath.section].{{ model_variable }}List[indexPath.row]
            }
            .do(onNext: navigator.to{{ model_name }}Detail)
            .mapToVoid()

        let isEmpty = checkIfDataIsEmpty(trigger: Driver.merge(isLoading, isReloading),
                                         items: {{ model_variable }}Sections)

        return Output(
            error: error,
            isLoading: isLoading,
            isReloading: isReloading,
            isLoadingMore: isLoadingMore,
            {{ model_variable }}Sections: {{ model_variable }}Sections,
            selected{{ model_name }}: selected{{ model_name }},
            isEmpty: isEmpty
        )
    }
}
