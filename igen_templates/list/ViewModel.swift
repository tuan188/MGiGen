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
        let fetchItems: Driver<Void>
        let {{ model_variable }}List: Driver<[{{ model_name }}]>
        let selected{{ model_name }}: Driver<Void>
        let isEmpty: Driver<Bool>
    }

    func transform(_ input: Input) -> Output {
        let configOutput = configPagination(
            loadTrigger: input.loadTrigger,
            reloadTrigger: input.reloadTrigger,
            loadMoreTrigger: input.loadMoreTrigger,
            getItems: useCase.get{{ model_name }}List)

        let (page, fetchItems, loadError, isLoading, isReloading, isLoadingMore) = configOutput

        let {{ model_variable }}List = page
            .map { $0.items.map { $0 } }
            .asDriverOnErrorJustComplete()

        let selected{{ model_name }} = input.select{{ model_name }}Trigger
            .withLatestFrom({{ model_variable }}List) {
                return ($0, $1)
            }
            .map { indexPath, {{ model_variable }}List in
                return {{ model_variable }}List[indexPath.row]
            }
            .do(onNext: { {{ model_variable }} in
                self.navigator.to{{ model_name }}Detail({{ model_variable }}: {{ model_variable }})
            })
            .mapToVoid()

        let isEmpty = Driver.combineLatest(fetchItems, Driver.merge(isLoading, isReloading))
            .withLatestFrom({{ model_variable }}List) { ($0.1, $1.isEmpty) }
            .map { isLoading, isEmpty -> Bool in
                if isLoading { return false }
                return isEmpty
            }

        return Output(
            error: loadError,
            isLoading: isLoading,
            isReloading: isReloading,
            isLoadingMore: isLoadingMore,
            fetchItems: fetchItems,
            {{ model_variable }}List: {{ model_variable }}List,
            selected{{ model_name }}: selected{{ model_name }},
            isEmpty: isEmpty
        )
    }
}
