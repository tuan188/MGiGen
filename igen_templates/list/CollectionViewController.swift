import UIKit
import Reusable

final class {{ name }}ViewController: UIViewController, BindableType {
    
    // MARK: - IBOutlets
    
    @IBOutlet weak var collectionView: LoadMoreCollectionView!

    // MARK: - Properties
    
    var viewModel: {{ name }}ViewModel!

    fileprivate struct Options {
        var itemSpacing: CGFloat = 8
        var lineSpacing: CGFloat = 8
        var itemsPerRow: Int = 2
        var sectionInsets = UIEdgeInsets(
            top: 10.0,
            left: 10.0,
            bottom: 10.0,
            right: 10.0
        )
    }

    fileprivate var options = Options()

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
            $0.alwaysBounceVertical = true
        }
        collectionView.rx
            .setDelegate(self)
            .disposed(by: rx.disposeBag)
    }

    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(
            loadTrigger: Driver.just(()),
            reloadTrigger: collectionView.refreshTrigger,
            loadMoreTrigger: collectionView.loadMoreTrigger,
            select{{ model_name }}Trigger: collectionView.rx.itemSelected.asDriver()
        )

        let output = viewModel.transform(input)
        
        output.{{ model_variable }}List
            .drive(collectionView.rx.items) { collectionView, index, {{ model_variable }} in
                return collectionView.dequeueReusableCell(
                    for: IndexPath(row: index, section: 0),
                    cellType: {{ model_name }}Cell.self)
                    .then {
                        $0.bindViewModel({{ model_name }}ViewModel({{ model_variable }}: {{ model_variable }}))
                    }
            }
            .disposed(by: rx.disposeBag)
        output.error
            .drive(rx.error)
            .disposed(by: rx.disposeBag)
        output.loading
            .drive(rx.isLoading)
            .disposed(by: rx.disposeBag)
        output.refreshing
            .drive(collectionView.refreshing)
            .disposed(by: rx.disposeBag)
        output.loadingMore
            .drive(collectionView.loadingMore)
            .disposed(by: rx.disposeBag)
        output.fetchItems
            .drive()
            .disposed(by: rx.disposeBag)
        output.selected{{ model_name }}
            .drive()
            .disposed(by: rx.disposeBag)
        output.isEmptyData
            .drive()
            .disposed(by: rx.disposeBag)
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
        let screenSize = UIScreen.main.bounds
        let paddingSpace = options.sectionInsets.left
            + options.sectionInsets.right
            + CGFloat(options.itemsPerRow - 1) * options.itemSpacing
        let availableWidth = screenSize.width - paddingSpace
        let widthPerItem = availableWidth / CGFloat(options.itemsPerRow)
        let heightPerItem = widthPerItem
        return CGSize(width: widthPerItem, height: heightPerItem)
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        insetForSectionAt section: Int) -> UIEdgeInsets {
        return options.sectionInsets
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return options.lineSpacing
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return options.itemSpacing
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}
