import MGArchitecture
import MGLoadMore
import Reusable
import RxCocoa
import RxSwift
import Then
import UIKit

final class {{ name }}ViewController: UIViewController, Bindable {

    // MARK: - IBOutlets

    @IBOutlet weak var collectionView: PagingCollectionView!

    // MARK: - Properties

    var viewModel: {{ name }}ViewModel!
    var disposeBag = DisposeBag()

    private var {{ model_variable }}List = [{{ model_name }}ItemViewModel]()

    struct LayoutOptions {
        var itemSpacing: CGFloat = 16
        var lineSpacing: CGFloat = 16
        var itemsPerRow: Int = 2

        var sectionInsets = UIEdgeInsets(
            top: 16.0,
            left: 16.0,
            bottom: 16.0,
            right: 16.0
        )

        var itemSize: CGSize {
            let screenSize = UIScreen.main.bounds

            let paddingSpace = sectionInsets.left
                + sectionInsets.right
                + CGFloat(itemsPerRow - 1) * itemSpacing

            let availableWidth = screenSize.width - paddingSpace
            let widthPerItem = availableWidth / CGFloat(itemsPerRow)
            let heightPerItem = widthPerItem

            return CGSize(width: widthPerItem, height: heightPerItem)
        }
    }

    private var layoutOptions = LayoutOptions()

    // MARK: - Life Cycle

    override func viewDidLoad() {
        super.viewDidLoad()
        configView()
    }

    deinit {
        logDeinit()
    }

    // MARK: - Methods

    private func configView() {
        collectionView.do {
            $0.register(cellType: {{ model_name }}Cell.self)
            $0.delegate = self
            $0.prefetchDataSource = self
            $0.alwaysBounceVertical = true
            {% if not paging %}
            $0.refreshFooter = nil
            {% endif %}
        }
    }

    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(
            loadTrigger: Driver.just(()),
            reloadTrigger: collectionView.refreshTrigger,
            {% if paging %}
            loadMoreTrigger: collectionView.loadMoreTrigger,
            {% endif %}
            select{{ model_name }}Trigger: collectionView.rx.itemSelected.asDriver()
        )

        let output = viewModel.transform(input, disposeBag: disposeBag)

        output.${{ model_variable }}List
            .asDriver()
            .do(onNext: { [unowned self] {{ model_variable }}List in
                self.{{ model_variable }}List = {{ model_variable }}List
            })
            .drive(collectionView.rx.items) { collectionView, row, {{ model_variable }} in
                return collectionView.dequeueReusableCell(
                    for: IndexPath(row: row, section: 0),
                    cellType: {{ model_name }}Cell.self
                )
                .then {
                    $0.bindViewModel({{ model_variable }})
                }
            }
            .disposed(by: disposeBag)

        output.$error
            .asDriver()
            .unwrap()
            .drive(rx.error)
            .disposed(by: disposeBag)

        output.$isLoading
            .asDriver()
            .drive(rx.isLoading)
            .disposed(by: disposeBag)

        output.$isReloading
            .asDriver()
            .drive(collectionView.isRefreshing)
            .disposed(by: disposeBag)

        {% if paging %}
        output.$isLoadingMore
            .asDriver()
            .drive(collectionView.isLoadingMore)
            .disposed(by: disposeBag)

        {% endif %}
        output.$isEmpty
            .asDriver()
            .drive()
            .disposed(by: disposeBag)
    }

}

// MARK: - Binders
extension {{ name }}ViewController {

}

// MARK: - UICollectionViewDelegate
extension {{ name }}ViewController: UICollectionViewDelegate, UICollectionViewDelegateFlowLayout {
    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        sizeForItemAt indexPath: IndexPath) -> CGSize {
        // Set Collection View's Estimate Size to None in Storyboard
        return layoutOptions.itemSize
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        insetForSectionAt section: Int) -> UIEdgeInsets {
        return layoutOptions.sectionInsets
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return layoutOptions.lineSpacing
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return layoutOptions.itemSpacing
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}

// MARK: - UICollectionViewDataSourcePrefetching
extension {{ name }}ViewController: UICollectionViewDataSourcePrefetching {
    func collectionView(_ collectionView: UICollectionView, prefetchItemsAt indexPaths: [IndexPath]) {

    }
    
    func collectionView(_ collectionView: UICollectionView, cancelPrefetchingForItemsAt indexPaths: [IndexPath]) {
        
    }
}
