import MGArchitecture
import RxCocoa
import RxSwift
import UIKit

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
        @Property var {{ model_variable }}List = [{{ model_name }}ItemViewModel]()
        @Property var isEmpty = false
    }

    func transform(_ input: Input, disposeBag: DisposeBag) -> Output {
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
                                        getItems: useCase.get{{ model_name }}List)

        let getListResult = getList(input: getListInput)
        let ({{ model_variable }}List, error, isLoading, isReloading) = getListResult.destructured
        {% endif %}

        {{ model_variable }}List
            .map { $0.map({{ model_name }}ItemViewModel.init) }
            .drive(output.${{ model_variable }}List)
            .disposed(by: disposeBag)

        {% if paging %}
        select(trigger: input.select{{ model_name }}Trigger, items: {{ model_variable }}List)
            .drive(onNext: navigator.to{{ model_name }}Detail)
            .disposed(by: disposeBag)

        checkIfDataIsEmpty(trigger: Driver.merge(isLoading, isReloading),
                           items: {{ model_variable }}List)
            .drive(output.$isEmpty)
            .disposed(by: disposeBag)
        {% else %}
        select(trigger: input.select{{ model_name }}Trigger, items: {{ model_variable }}List)
            .drive(onNext: navigator.to{{ model_name }}Detail)
            .disposed(by: disposeBag)

        checkIfDataIsEmpty(trigger: Driver.merge(isLoading, isReloading),
                           items: {{ model_variable }}List)
            .drive(output.$isEmpty)
            .disposed(by: disposeBag)
        {% endif %}

        error
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
