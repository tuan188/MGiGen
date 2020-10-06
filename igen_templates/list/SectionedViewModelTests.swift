@testable import {{ project }}
import RxSwift
import XCTest

final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!

    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!

    private var disposeBag: DisposeBag!

    private let loadTrigger = PublishSubject<Void>()
    private let reloadTrigger = PublishSubject<Void>()
    {% if paging %}
    private let loadMoreTrigger = PublishSubject<Void>()
    {% endif %}
    private let select{{ model_name }}Trigger = PublishSubject<IndexPath>()

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase)

        input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete(),
            reloadTrigger: reloadTrigger.asDriverOnErrorJustComplete(),
            {% if paging %}
            loadMoreTrigger: loadMoreTrigger.asDriverOnErrorJustComplete(),
            {% endif %}
            select{{ model_name }}Trigger: select{{ model_name }}Trigger.asDriverOnErrorJustComplete()
        )

        disposeBag = DisposeBag()
        output = viewModel.transform(input, disposeBag: disposeBag)
    }

    func test_loadTrigger_get{{ model_name }}List() {
        // act
        loadTrigger.onNext(())

        // assert
        XCTAssert(useCase.get{{ model_name }}ListCalled)
        XCTAssertEqual(output.{{ model_variable }}Sections[0].{{ model_variable }}List.count, 1)
    }

    func test_loadTrigger_get{{ model_name }}List_failedShowError() {
        // arrange
        useCase.get{{ model_name }}ListReturnValue = Observable.error(TestError())

        // act
        loadTrigger.onNext(())

        // assert
        XCTAssert(useCase.get{{ model_name }}ListCalled)
        XCTAssert(output.error is TestError)
    }

    func test_reloadTrigger_get{{ model_name }}List() {
        // act
        reloadTrigger.onNext(())

        // assert
        XCTAssert(useCase.get{{ model_name }}ListCalled)
        XCTAssertEqual(output.{{ model_variable }}Sections[0].{{ model_variable }}List.count, 1)
    }

    func test_reloadTrigger_get{{ model_name }}List_failedShowError() {
        // arrange
        useCase.get{{ model_name }}ListReturnValue = Observable.error(TestError())

        // act
        reloadTrigger.onNext(())

        // assert
        XCTAssert(useCase.get{{ model_name }}ListCalled)
        XCTAssert(output.error is TestError)
    }

    func test_reloadTrigger_notGet{{ model_name }}ListIfStillLoading() {
        // arrange
        useCase.get{{ model_name }}ListReturnValue = Observable.never()

        // act
        loadTrigger.onNext(())
        useCase.get{{ model_name }}ListCalled = false
        reloadTrigger.onNext(())

        // assert
        XCTAssertFalse(useCase.get{{ model_name }}ListCalled)
    }

    func test_reloadTrigger_notGet{{ model_name }}ListIfStillReloading() {
        // arrange
        useCase.get{{ model_name }}ListReturnValue = Observable.never()

        // act
        reloadTrigger.onNext(())
        useCase.get{{ model_name }}ListCalled = false
        reloadTrigger.onNext(())

        // assert
        XCTAssertFalse(useCase.get{{ model_name }}ListCalled)
    }

    {% if paging %}
    func test_loadMoreTrigger_loadMore{{ model_name }}List() {
        // act
        loadTrigger.onNext(())
        useCase.get{{ model_name }}ListCalled = false
        loadMoreTrigger.onNext(())

        // assert
        XCTAssert(useCase.get{{ model_name }}ListCalled)
        XCTAssertEqual(output.{{ model_variable }}Sections[0].{{ model_variable }}List.count, 2)
    }

    func test_loadMoreTrigger_loadMore{{ model_name }}List_failedShowError() {
        // act
        loadTrigger.onNext(())
        useCase.get{{ model_name }}ListReturnValue = Observable.error(TestError())
        loadMoreTrigger.onNext(())

        // assert
        XCTAssert(output.error is TestError)
    }

    func test_loadMoreTrigger_notLoadMore{{ model_name }}ListIfStillLoading() {
        // arrange
        useCase.get{{ model_name }}ListReturnValue = Observable.never()

        // act
        loadTrigger.onNext(())
        useCase.get{{ model_name }}ListCalled = false
        loadMoreTrigger.onNext(())

        // assert
        XCTAssertFalse(useCase.get{{ model_name }}ListCalled)
    }

    func test_loadMoreTrigger_notLoadMore{{ model_name }}ListIfStillReloading() {
        // arrange
        useCase.get{{ model_name }}ListReturnValue = Observable.never()

        // act
        reloadTrigger.onNext(())
        useCase.get{{ model_name }}ListCalled = false
        loadMoreTrigger.onNext(())

        // assert
        XCTAssertFalse(useCase.get{{ model_name }}ListCalled)
    }

    func test_loadMoreTrigger_notLoadMore{{ model_name }}ListStillLoadingMore() {
        // arrange
        useCase.get{{ model_name }}ListReturnValue = Observable.never()

        // act
        loadMoreTrigger.onNext(())
        useCase.get{{ model_name }}ListCalled = false
        loadMoreTrigger.onNext(())

        // assert
        XCTAssertFalse(useCase.get{{ model_name }}ListCalled)
    }

    {% endif %}
    func test_select{{ model_name }}Trigger_to{{ model_name }}Detail() {
        // act
        loadTrigger.onNext(())
        select{{ model_name }}Trigger.onNext(IndexPath(row: 0, section: 0))

        // assert
        XCTAssert(navigator.to{{ model_name }}DetailCalled)
    }
}
