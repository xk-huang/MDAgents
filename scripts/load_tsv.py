import click
import pandas as pd
import json
from pathlib import Path

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--debug', is_flag=True, help="Enable debug mode.")
def load_tsv(file_path, debug):
    
    # Load the TSV file into a pandas DataFrame
    df = pd.read_csv(file_path, sep='\t')
    
    # Display the first few rows of the DataFrame
    click.echo("Loaded TSV file successfully. Here are the first few rows:")
    # click.echo(df.head().to_string(index=False))
    click.echo(f"Number of rows: {len(df)}")

    # save a row to json
    sample_dir = Path("misc")
    sample_dir.mkdir(parents=True, exist_ok=True)
    sample_json_path = sample_dir / "sample.json"
    with open(sample_json_path, "w") as f:
        json.dump(df.iloc[0].to_dict(), f, indent=2)
    click.echo(f"Sample row saved to {sample_json_path}")
        
    if debug:
        click.echo("Debug mode enabled.")
        click.echo(f"Attempting to load file: {file_path}")
        # fmt: off
        import IPython; IPython.embed()
        # fmt: on


if __name__ == '__main__':
    load_tsv()