import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from beam_nuggets.io import kafkaio
import apache_beam.transforms.window as window
import re

consumer_config = {"topic": "topic_test",
                   "bootstrap_servers": "localhost:9092",
                   "group_id": "view streaming data"}

'''
with beam.Pipeline(options=PipelineOptions()) as p:
    notifications = p | "Reading messages from Kafka" >> kafkaio.KafkaConsume(
        consumer_config=consumer_config,
        value_decoder=bytes.decode,  # optional
    )
    notifications | 'Writing to stdout' >> beam.Map(print)
'''

regex = r'(?P<icon>[^\s,]+), *(\w+), *(\w+)'

def run_pipeline():
  # Load pipeline options from the script's arguments
  options = PipelineOptions()
  # Create a pipeline and run it after leaving the 'with' block
  with beam.Pipeline(options=options) as p:
    # Wrap in paranthesis to avoid Python indention issues
    (p
     # Load some dummy data, this can be replaced with a proper source later on
     | "Reading product views from Kafka" >> kafkaio.KafkaConsume(consumer_config=consumer_config, value_decoder=bytes.decode)
     # Split the words into one element per word
     #| 'Split words' >> beam.FlatMap(lambda words: str(words).split(','))
     | 'Split words 2' >> beam.Map(lambda words: (re.sub('[^0-9]','',str(words).split(",")[2]), 1))
     # We are assigning a count of 1 to every word (very relevant if we had more data)
     # We are interested in 10 second periods of words
     | 'Window of 10 seconds' >> beam.WindowInto(window.FixedWindows(10))
     # Group all the values (counts) of each unique word
     #| 'Pair with 2' >> beam.Map(lambda word: (str(word), 1))
     #| 'Group by key' >> beam.GroupByKey()
     # Sum the counts for each word and return the result
     #| 'Sum word counts' >> beam.Map(lambda kv: (kv[0], sum(kv[1])))
     # Just print to the console for testing
     | 'Print to console' >> beam.Map(lambda wordcount: print(wordcount))
    )

if __name__ == '__main__':
  run_pipeline()
        