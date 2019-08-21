@testable import {{ project }}
import XCTest
import RxSwift
import RxBlocking

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

        output = viewModel.transform(input)

        disposeBag = DisposeBag()

        output.error.drive().disposed(by: disposeBag)
        output.isLoading.drive().disposed(by: disposeBag)
        output.isReloading.drive().disposed(by: disposeBag)
        {% if paging %}
        output.isLoadingMore.drive().disposed(by: disposeBag)
        {% endif %}
        output.{{ model_variable }}Sections.drive().disposed(by: disposeBag)
        output.selected{{ model_name }}.drive().disposed(by: disposeBag)
        output.isEmpty.drive().disposed(by: disposeBag)
    }

    func test_loadTrigger_get{{ model_name }}List() {
        // act
        loadTrigger.onNext(())
        let {{ model_variable }}Sections = try? output.{{ model_variable }}Sections.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(useCase.get{{ model_name }}ListCalled)
        XCTAssertEqual({{ model_variable }}Sections?[0].{{ model_variable }}List.count, 1)
    }

    func test_loadTrigger_get{{ model_name }}List_failedShowError() {
        // arrange
        useCase.get{{ model_name }}ListReturnValue = Observable.error(TestError())

        // act
        loadTrigger.onNext(())
        let error = try? output.error.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(useCase.get{{ model_name }}ListCalled)
        XCTAssert(error is TestError)
    }

    func test_reloadTrigger_get{{ model_name }}List() {
        // act
        reloadTrigger.onNext(())
        let {{ model_variable }}Sections = try? output.{{ model_variable }}Sections.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(useCase.get{{ model_name }}ListCalled)
        XCTAssertEqual({{ model_variable }}Sections?[0].{{ model_variable }}List.count, 1)
    }

    func test_reloadTrigger_get{{ model_name }}List_failedShowError() {
        // arrange
        useCase.get{{ model_name }}ListReturnValue = Observable.error(TestError())

        // act
        reloadTrigger.onNext(())
        let error = try? output.error.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(useCase.get{{ model_name }}ListCalled)
        XCTAssert(error is TestError)
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
        let {{ model_variable }}Sections = try? output.{{ model_variable }}Sections.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(useCase.get{{ model_name }}ListCalled)
        XCTAssertEqual({{ model_variable }}Sections?[0].{{ model_variable }}List.count, 2)
    }

    func test_loadMoreTrigger_loadMore{{ model_name }}List_failedShowError() {
        // act
        loadTrigger.onNext(())
        useCase.get{{ model_name }}ListReturnValue = Observable.error(TestError())
        loadMoreTrigger.onNext(())
        let error = try? output.error.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(error is TestError)
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
