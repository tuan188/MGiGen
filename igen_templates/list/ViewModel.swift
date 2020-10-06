import MGArchitecture
import RxSwift
import RxCocoa

struct {{ name }}ViewModel {
    let navigator: {{ name }}NavigatorType
    let useCase: {{ name }}UseCaseType
}

// MARK: - ViewModel
extension {{ name }}ViewModel: ViewModel {
    struct Input {
        let loadTrigger: Driver<Void>
        let reloadTrigger: Driver<Void>
        {% if paging %}
        let loadMoreTrigger: Driver<Void>
        {% endif %}
        let select{{ model_name }}Trigger: Driver<IndexPath>
    }

    struct Output {
        @Property var error: Error?
        @Property var isLoading = false
        @Property var isReloading = false
        {% if paging %}
        @Property var isLoadingMore = false
        {% endif %}
        @Property var {{ model_variable }}List = [{{ model_name }}ViewModel]()
        @Property var isEmpty = false
    }

    func transform(_ input: Input) -> Output {
        let output = Output()

        {% if paging %}
        let getPageInput = GetPageInput(loadTrigger: input.loadTrigger,
                                        reloadTrigger: input.reloadTrigger,
                                        loadMoreTrigger: input.loadMoreTrigger,
                                        getItems: useCase.get{{ model_name }}List(page:))

        let getPageResult = getPage(input: getPageInput)
        let (page, error, isLoading, isReloading, isLoadingMore) = getPageResult.destructured

        let {{ model_variable }}List = page
            .map { $0.items }
        {% else %}
        let getListInput = GetListInput(loadTrigger: input.loadTrigger,
                                        reloadTrigger: input.reloadTrigger,
                                        loadMoreTrigger: input.loadMoreTrigger,
                                        getItems: useCase.get{{ model_name }}List(page:))

        let getListResult = getList(input: getListInput)
        let ({{ model_variable }}List, error, isLoading, isReloading) = getListResult.destructured
        {% endif %}

        let {{ model_variable }}ViewModelList = {{ model_variable }}List
            .map { $0.map({{ model_name }}ViewModel.init) }

        select(trigger: input.select{{ model_name }}Trigger, items: {{ model_variable }}List)
            .drive(onNext: navigator.to{{ model_name }}Detail)
            .disposed(by: disposeBag)

        checkIfDataIsEmpty(trigger: Driver.merge(isLoading, isReloading),
                           items: {{ model_variable }}Sections)

        pagingError
            .drive(output.$error)
            .disposed(by: disposeBag)
        
        isLoading
            .drive(output.$isLoading)
            .disposed(by: disposeBag)
        
        isReloading
            .drive(output.$isReloading)
            .disposed(by: disposeBag)

        {% if paging %}
        isLoadingMore
            .drive(output.$isLoadingMore)
            .disposed(by: disposeBag)

        {% endif %}
        return output
    }
}
