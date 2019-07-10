@testable import {{ project }}
import RxSwift

final class {{ name }}UseCaseMock: {{ name }}UseCaseType {

    // MARK: - get{{ model_name }}List

    var get{{ model_name }}ListCalled = false

    var get{{ model_name }}ListReturnValue: Observable<PagingInfo<{{ model_name }}>> = {
        let items = [
            {{ model_name }}().with { $0.id = 1 }
        ]
        let page = PagingInfo<{{ model_name }}>(page: 1, items: items)
        return Observable.just(page)
    }()

    func get{{ model_name }}List(page: Int) -> Observable<PagingInfo<{{ model_name }}>> {
        get{{ model_name }}ListCalled = true
        return get{{ model_name }}ListReturnValue
    }
}
