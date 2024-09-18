import '../assets/styles.css'

const SearchBox = () => {
    return (
        <div className="search-box">
            <input
                type="text"
                placeholder="Enter keywords..."
            />
            <button className="search-btn">
            </button>
        </div>
    );
}

export default SearchBox;