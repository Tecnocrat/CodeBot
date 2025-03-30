from metadata_extractor import list_files_and_metadata, save_structure_to_json

def self_audit():
    """
    CodeBot generates a snapshot of its own structure and metadata.
    """
    base_dir = "C:\\dev\\CodeBot"
    metadata_file = get_versioned_filename(base_dir, "basecode_metadata", ".json")
    metadata = list_files_and_metadata(base_dir)
    save_structure_to_json(metadata, metadata_file)

if __name__ == "__main__":
    self_audit()
