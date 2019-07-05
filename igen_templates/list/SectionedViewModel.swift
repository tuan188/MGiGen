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
        let isRefreshing: Driver<Bool>
        let isLoadingMore: Driver<Bool>
        let fetchItems: Driver<Void>
        let {{ model_variable }}Sections: Driver<[{{ model_name }}Section]>
        let selected{{ model_name }}: Driver<Void>
        let isEmpty: Driver<Bool>
    }

    struct {{ model_name }}Section {
        let header: String
        let {{ model_variable }}List: [{{ model_name }}]
    }

    func transform(_ input: Input) -> Output {
        let loadMoreOutput = setupLoadMorePaging(
            loadTrigger: input.loadTrigger,
            getItems: useCase.get{{ model_name }}List,
            refreshTrigger: input.reloadTrigger,
            refreshItems: useCase.get{{ model_name }}List,
            loadMoreTrigger: input.loadMoreTrigger,
            loadMoreItems: useCase.loadMore{{ model_name }}List)

        let (page, fetchItems, loadError, isLoading, isRefreshing, isLoadingMore) = loadMoreOutput

        let {{ model_variable }}Sections = page
            .map { $0.items.map { $0 } }
            .map { [{{ model_name }}Section(header: "Section1", {{ model_variable }}List: $0)] }
            .asDriverOnErrorJustComplete()

        let selected{{ model_name }} = input.select{{ model_name }}Trigger
            .withLatestFrom({{ model_variable }}Sections) {
                return ($0, $1)
            }
            .map { params -> {{ model_name }} in
                let (indexPath, {{ model_variable }}Sections) = params
                return {{ model_variable }}Sections[indexPath.section].{{ model_variable }}List[indexPath.row]
            }
            .do(onNext: { {{ model_variable }} in
                self.navigator.to{{ model_name }}Detail({{ model_variable }}: {{ model_variable }})
            })
            .mapToVoid()

        let isEmpty = Driver.combineLatest(fetchItems, Driver.merge(isLoading, isRefreshing))
            .withLatestFrom({{ model_variable }}Sections) { ($0.1, $1.isEmpty) }
            .map { args -> Bool in
                let (isLoading, isEmpty) = args
                if isLoading { return false }
                return isEmpty
            }

        return Output(
            error: loadError,
            isLoading: isLoading,
            isRefreshing: isRefreshing,
            isLoadingMore: isLoadingMore,
            fetchItems: fetchItems,
            {{ model_variable }}Sections: {{ model_variable }}Sections,
            selected{{ model_name }}: selected{{ model_name }},
            isEmpty: isEmpty
        )
    }
}
