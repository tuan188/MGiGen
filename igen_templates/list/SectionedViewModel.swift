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
        @Property var {{ model_variable }}Sections = [{{ model_name }}SectionViewModel]()
        @Property var isEmpty = false
    }

    struct {{ model_name }}Section {
        let header: String
        let {{ model_variable }}List: [{{ model_name }}]
    }

    struct {{ model_name }}SectionViewModel {
        let header: String
        let {{ model_variable }}List: [{{ model_name }}ItemViewModel]
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

        let {{ model_variable }}Sections = page
            .map { $0.items }
            .map { [{{ model_name }}Section(header: "Section1", {{ model_variable }}List: $0)] }
        {% else %}
        let getListInput = GetListInput(loadTrigger: input.loadTrigger,
                                        reloadTrigger: input.reloadTrigger,
                                        getItems: useCase.get{{ model_name }}List)

        let getListResult = getList(input: getListInput)
        let ({{ model_variable }}List, error, isLoading, isReloading) = getListResult.destructured

        let {{ model_variable }}Sections = {{ model_variable }}List
            .map { [{{ model_name }}Section(header: "Section1", {{ model_variable }}List: $0)] }
        {% endif %}

        {{ model_variable }}Sections
            .map {
                return $0.map { section in
                    return {{ model_name }}SectionViewModel(
                        header: section.header, 
                        {{ model_variable }}List: section.{{ model_variable }}List.map({{ model_name }}ItemViewModel.init)
                    )
                }
            }
            .drive(output.${{ model_variable }}Sections)
            .disposed(by: disposeBag)

        input.select{{ model_name }}Trigger
            .withLatestFrom({{ model_variable }}Sections) {
                return ($0, $1)
            }
            .map { indexPath, {{ model_variable }}Sections -> {{ model_name }} in
                return {{ model_variable }}Sections[indexPath.section].{{ model_variable }}List[indexPath.row]
            }
            .drive(onNext: navigator.to{{ model_name }}Detail)
            .disposed(by: disposeBag)

        checkIfDataIsEmpty(trigger: Driver.merge(isLoading, isReloading),
                           items: {{ model_variable }}Sections)
            .drive(output.$isEmpty)
            .disposed(by: disposeBag)

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
