
/** Check whether if an address is a contract
 */
function exists(address what) view returns (bool) {
    uint size;
    assembly {
        size := extcodesize(what)
    }
    return size > 0;
}